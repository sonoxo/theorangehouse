import argparse, json
from .api import serve
from .model import Scenario, project
def main():
    parser=argparse.ArgumentParser(prog="orangehouse"); sub=parser.add_subparsers(dest="command",required=True)
    api=sub.add_parser("serve"); api.add_argument("--host",default="127.0.0.1"); api.add_argument("--port",type=int,default=8080)
    run=sub.add_parser("project"); run.add_argument("starting_value",type=float); run.add_argument("--monthly-flow",type=float,default=0); run.add_argument("--annual-rate",type=float,default=0); run.add_argument("--volatility",type=float,default=0); run.add_argument("--months",type=int,default=12)
    args=parser.parse_args()
    if args.command=="serve": serve(args.host,args.port)
    else: print(json.dumps(project(Scenario(args.starting_value,args.monthly_flow,args.annual_rate,args.volatility,args.months)),indent=2))
if __name__ == "__main__": main()
