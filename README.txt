Data sourced from NIST had values randomized so that it is synthetic (because it is under liscence) and no matching data exists in this project
src/upload_to_scitrack will populate entire database with data as specifeid in .json files under data directory
    add to this script as more dat is prepared so you only hadve to run the one
extra src files are for data aquisition/preperation
in the end to create the DB just have mysql downloaded and in path, then run sql_scripts/SciTrackV1.sql to create DB
then go to src/upload_to_scitrack, change connector username/password to match yours (I just use root) then run that script and db should be good

