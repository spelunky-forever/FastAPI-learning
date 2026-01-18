import argparse
import os

from dotenv import load_dotenv
import uvicorn

if __name__=="__main__":
    parser=argparse.ArgumentParser(description="Run server in different modes.")

    app_mode = parser.add_argument_group(title="App modes",description="Run server in different modes.")
    app_mode.add_argument("--prod",action="store_true",help="Switch to prodution mode.")
    app_mode.add_argument("--test",action="store_true",help="Switch to test mode.")
    app_mode.add_argument("--dev",action="store_true",help="Switch to develope mode.")

    db_type = parser.add_argument_group(title="Database types",description="Run server with different database types.")
    db_type.add_argument("--db", help="Run the server in database type.", choices=["postgresql","mysql"], default="postgresql")

    args=parser.parse_args()

    if args.prod:
        load_dotenv("setting/.env.prod")
    elif args.test:
        load_dotenv("setting/.env.test")
    else:
        load_dotenv("setting/.env.dev")

    os.environ["DB_TYPE"] = args.db

    uvicorn.run("main:app",host="0.0.0.0",port=int(os.getenv("PORT")),reload=bool(os.getenv("RELOAD")))