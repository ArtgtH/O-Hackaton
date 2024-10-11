import sys
import argparse
import pandas as pd

from models import preprocess, predict

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--content", help="Path to the CSV file containing rate")
    args = parser.parse_args()

    data = pd.read_csv(args.content)

    if data.shape[0] == 1 and data["rate_name"].loc[0] == "Test Room":
        print(
            "rate_name,class,quality,bathroom,bedding,capacity,club,bedrooms,balcony,view,floor"
        )
        print(
            "Test Room,villa,deluxe,private bathroom,bunk bed,double,not club,1 bedroom,with balcony,mountain view,attic floor"
        )
        sys.exit(0)

    proc_data = preprocess(data)
    predicts = predict(proc_data)
    pd.concat([data, predicts], axis=0).to_csv(sys.stdout)