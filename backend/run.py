import argparse
import os

from dotenv import load_dotenv
import uvicorn

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Run server in different modes.")
    parser.add_argument("--prod",action="store_true",help="Switch to prodution mode.")
    parser.add_argument("--test",action="store_true",help="Switch to test mode.")
    parser.add_argument("--dev",action="store_true",help="Switch to develope mode.")
    args=parser.parse_args()

    if args.prod:
        load_dotenv("setting/.env.prod")
    elif args.test:
        load_dotenv("setting/.env.test")
    elif args.dev:
        load_dotenv("setting/.env.dev")

    uvicorn.run("main:app",host="0.0.0.0",port=int(os.getenv("PORT")),reload=bool(os.getenv("RELOAD")))