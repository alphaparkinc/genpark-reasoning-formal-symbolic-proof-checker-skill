# -*- coding: utf-8 -*-
"""
GenPark Reasoning Formal Symbolic Proof Checker MCP Server
Exposes formal symbolic logic assertion tools via JSON-RPC 2.0 over STDIO.
"""

import sys
import json
from client import GenParkReasoningFormalSymbolicProofChecker

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-reasoning-formal-symbolic-proof-checker", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "verify_deduction",
                        "description": "Evaluates propositional logic deduction validity: Premises |= Conclusion via exhaustive truth-table semantic entailment checking.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "premises": {
                                    "type": "array",
                                    "items": {"type": "string"}
                                },
                                "conclusion": {"type": "string"}
                            },
                            "required": ["premises", "conclusion"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "verify_deduction":
            checker = GenParkReasoningFormalSymbolicProofChecker()
            res = checker.verify_deduction(
                premises=args.get("premises", []),
                conclusion=args.get("conclusion", "Q")
            )
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}}
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": f"Method '{method}' not supported"}}

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("MCP Server Discovery Test OK")
        chk = GenParkReasoningFormalSymbolicProofChecker()
        test_res = chk.verify_deduction(["P -> Q", "P"], "Q")
        print(f"Test Modus Ponens: {test_res['is_deduction_valid']}")
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
