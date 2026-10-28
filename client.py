# -*- coding: utf-8 -*-
"""
GenPark Reasoning Formal Symbolic Proof Checker Client
Zero-dependency propositional logic assertion and formal symbolic deduction validator.
Zero external dependencies -- Python 3.9+ standard library only.
"""

import itertools
import re
from typing import Dict, Any, List

class GenParkReasoningFormalSymbolicProofChecker:
    """
    Evaluates propositional logic deduction validity:
    Premises |= Conclusion via exhaustive truth-table semantic entailment checking.
    Supports operators: NOT (!), AND (&), OR (|), IMPLIES (->), IFF (<->).
    """

    def __init__(self):
        pass

    def extract_variables(self, expressions: List[str]) -> List[str]:
        """Extracts unique propositional variables (e.g. P, Q, R)."""
        vars_set = set()
        for expr in expressions:
            found = re.findall(r'\b[A-Za-z][A-Za-z0-9_]*\b', expr)
            for v in found:
                if v.upper() not in ["AND", "OR", "NOT", "TRUE", "FALSE"]:
                    vars_set.add(v)
        return sorted(list(vars_set))

    def evaluate_expression(self, expr: str, assignment: Dict[str, bool]) -> bool:
        """
        Evaluates boolean formula under variable truth assignment.
        Converts -> and <-> to Python boolean logic.
        """
        cleaned = expr
        # Replace operators
        cleaned = cleaned.replace("<->", " == ")
        # A -> B is equivalent to (not A or B)
        # Handle simple IMPLIES replacements
        while "->" in cleaned:
            parts = cleaned.split("->", 1)
            left = parts[0].strip()
            right = parts[1].strip()
            cleaned = f"((not ({left})) or ({right}))"

        cleaned = re.sub(r'\bAND\b', 'and', cleaned, flags=re.I)
        cleaned = re.sub(r'\bOR\b', 'or', cleaned, flags=re.I)
        cleaned = re.sub(r'\bNOT\b', 'not', cleaned, flags=re.I)
        cleaned = cleaned.replace("!", " not ")
        cleaned = cleaned.replace("&", " and ")
        cleaned = cleaned.replace("|", " or ")

        # Substitute variable values
        for var, val in assignment.items():
            cleaned = re.sub(r'\b' + re.escape(var) + r'\b', str(val), cleaned)

        try:
            return bool(eval(cleaned, {"__builtins__": None}, {}))
        except Exception:
            return False

    def verify_deduction(
        self,
        premises: List[str],
        conclusion: str
    ) -> Dict[str, Any]:
        """
        Tests whether the premises semantically entail the conclusion.
        """
        all_exprs = premises + [conclusion]
        variables = self.extract_variables(all_exprs)

        if not variables:
            return {"error": "No propositional variables found"}

        counterexamples = []
        rows_checked = 0

        # Generate all 2^N truth assignments
        for combo in itertools.product([True, False], repeat=len(variables)):
            assignment = dict(zip(variables, combo))
            rows_checked += 1

            # Check if all premises evaluate to True
            premises_true = all(self.evaluate_expression(p, assignment) for p in premises)

            if premises_true:
                conc_val = self.evaluate_expression(conclusion, assignment)
                if not conc_val:
                    counterexamples.append({
                        "counterexample_assignment": assignment,
                        "premises_values": [self.evaluate_expression(p, assignment) for p in premises],
                        "conclusion_value": False
                    })

        is_valid = (len(counterexamples) == 0)

        return {
            "premises": premises,
            "conclusion": conclusion,
            "propositional_variables": variables,
            "truth_table_rows_evaluated": rows_checked,
            "is_deduction_valid": is_valid,
            "formal_proof_verdict": "LOGICALLY_VALID_TAUTOLOGY" if is_valid else "INVALID_FALLACY_DETECTED",
            "counterexamples_count": len(counterexamples),
            "sample_counterexample": counterexamples[0] if counterexamples else None
        }
