# -*- coding: utf-8 -*-
"""
Example usage of GenParkReasoningFormalSymbolicProofChecker
Demonstrates formal validation of Modus Ponens vs Affirming the Consequent fallacy.
"""

from client import GenParkReasoningFormalSymbolicProofChecker

def main():
    checker = GenParkReasoningFormalSymbolicProofChecker()

    cases = [
        {
            "name": "Case 1: Valid Modus Ponens (P -> Q, P |= Q)",
            "premises": ["P -> Q", "P"],
            "conclusion": "Q"
        },
        {
            "name": "Case 2: Fallacy of Affirming the Consequent (P -> Q, Q |= P)",
            "premises": ["P -> Q", "Q"],
            "conclusion": "P"
        },
        {
            "name": "Case 3: Hypothetical Syllogism (A -> B, B -> C |= A -> C)",
            "premises": ["A -> B", "B -> C"],
            "conclusion": "A -> C"
        }
    ]

    print("================================================================")
    print("GenPark Reasoning Formal Symbolic Proof Checker - Live Runs")
    print("================================================================\n")

    for c in cases:
        res = checker.verify_deduction(c["premises"], c["conclusion"])
        print(f"[{c['name']}]")
        print(f"  Premises              : {res['premises']}")
        print(f"  Conclusion            : {res['conclusion']}")
        print(f"  Validity Verdict      : {res['formal_proof_verdict']} (Valid: {res['is_deduction_valid']})")
        print(f"  Truth Table Rows      : {res['truth_table_rows_evaluated']} evaluated")
        if res['sample_counterexample']:
            print(f"  Falsifying Assignment : {res['sample_counterexample']['counterexample_assignment']}")
        print()

if __name__ == "__main__":
    main()
