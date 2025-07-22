""" Takes .msp files from NIST database, extracted with Lib2NIST, and stores relevant data in JSON file for easy updat to SQL DB
    in Lib2NIST we binned masses with options -> add the following term to all m/z before rounding : 0.3 """

from pathlib import Path
from datetime import datetime
import json
import random

class DBBuilder:

    def __init__(self,directory):
        """ Saves directory path as Path obj for easy utilization """
        self.directory = Path(directory)

    def parse_msp(self,file):
        """ Takes .msp file and converts each spectra to an entry in a json file """

        # create lists/dict to store records as we go
        records = []
        current_record = {}
        current_mzs = []
        current_intensities = []

        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()

                # if there is an empty line then the spectra data is done and move on to next spectra
                if not line:

                    # generate synthetic values for m/z and intensities to avoid legal issues with publishing
                    if current_mzs and current_intensities:
                        
                        # number of peaks in spectra (real)
                        num_peaks = len(current_mzs)
                        
                        # list of random, unique int m/z values to replace real data
                        random_mzs = random.sample(range(1,999),num_peaks)

                        # list of random intensity values to replace real data
                        random_ints = [random.randint(1,9999) for _ in range(num_peaks)]                    
                        
                        # make sure m/z list and intensity list are same length, then save fake data
                        if len(random_mzs) == len(random_ints):
                            current_record["mzs"] = random_mzs
                            current_record["intensities"] = random_ints

                        # print an error in case I messed up
                        else:
                            print("Error Generating Synthetic data")

                    # append current spectra info to records list
                    records.append(current_record)

                    # reset current_record peak info lists
                    current_record = {}
                    current_mzs = []
                    current_intensities = []
                    continue

                # grab the data from key:value pairs
                if ':' in line:

                    # identify key,value pairs
                    key,value = line.split(':',1)

                    # strip keys and values to get clean string
                    key = key.strip()
                    value = value.strip()

                    # store key value parirs
                    current_record[key] = value

                # if no ':' present then it is the m/z intensity pairs
                else:

                    # split the line at the space
                    mz,intensity = line.split(' ',1)

                    # store the m/z and intesnty values
                    current_mzs.append(int(mz))
                    current_intensities.append(int(intensity))

        # return records list
        return records

    def combine_to_json(self,output_json):
        """ Goes over all files in directory, removes data, and stores it all in one large json file """

        # grab directory and start a list for all records to combine
        directory = self.directory
        all_records = []

        # for every file that ends in .msp first parse then add it to the all_records list
        for file in directory.glob(f"*.msp"):

            # print message to ensure we can see if it fails
            print(f"Parsing {file}...")

            # save records
            record = self.parse_msp(file)

            # notify file has been parsed
            print(f"file {file} parsed")

            # add record to records
            all_records.extend(record)

        # change output to Path object
        output_path = Path(output_json)

        # open output and dump data to it
        with output_path.open('w',encoding='utf-8') as out:
            json.dump(all_records,out,indent=2)

        # print confirmation message
        print(f"Saved {len(all_records)} spectra to {output_path}")


    def compare_json_to_msp(self, json_file, msp_file):
        """
        Compare the randomized JSON spectra to the original MSP spectra
        and print whether each spectrum has been randomized.
        """

        # initialize counter to see how many spectra match
        count = 0

        # Load JSON randomized data
        with open(json_file, 'r', encoding='utf-8') as f:
            randomized_records = json.load(f)

        # Parse original MSP file with your existing parser (no randomization here)
        original_records = self.parse_msp(msp_file)

        # Compare each spectrum
        for i, (orig, rand) in enumerate(zip(original_records, randomized_records)):
            orig_mzs = orig.get("mzs", [])
            rand_mzs = rand.get("mzs", [])
            orig_ints = orig.get("intensities", [])
            rand_ints = rand.get("intensities", [])

            if orig_mzs == rand_mzs and orig_ints == rand_ints:
                count += 1
        
        print(f"{count} spectral matches between {msp_file} and {json_file}")


if __name__ == "__main__":

    #get datetime when data extraction is started
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")

    # input directory
    dir = r"C:\Jack\Extracted NIST"

    # msp file for comparison
    msp_file = r"C:\Jack\Extracted NIST\scitrack_example_input(real).MSP"

    # output path and name
    output = Path(r"C:\Jack\code\SciTrack\data") / f"{timestamp}_syntehtic_spectra.json"

    # build DB and ouptut json results
    builder = DBBuilder(dir)
    builder.combine_to_json(output)

    # compare falsified to real data (hopfeully 0 matches)
    builder.compare_json_to_msp(str(output), msp_file)