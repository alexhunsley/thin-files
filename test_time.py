import datetime
import time
import os
import stat

print("\n")

gmtime = time.gmtime()
localtime = time.localtime()


filePath = "test_time.py"

fileStatsObj = os.stat(filePath)
modificationTimeC = time.ctime ( fileStatsObj[stat.ST_MTIME] )
print("Full stats obj: ", fileStatsObj)

# this is in localtime
print(f"modificationTimeC this script = {modificationTimeC}  (secs = {fileStatsObj[stat.ST_MTIME]})")


modTimeSinceEpoch = os.path.getmtime(filePath)
# Convert seconds since epoch to readable timestamp
modificationTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modTimeSinceEpoch))
 
print("Last Modified Time via strftime : ", modificationTime, "  (secs = ", modTimeSinceEpoch)


# BOTH ways of getting file mod times in epoch time above are indeed epoch times, UTC - no offset.

# and this 'now' time below also returns epoch.
nowTime = time.time()
print("nowTime epoch = ", nowTime)




# print(f"\ngmtime = {gmtime}\nlocaltime = {localtime}")

# file_mtime = os.path.getmtime("test_time.py")

# print(f"mtime for this script = {file_mtime}\n")

# date_time_str = '2018-06-29 08:15:27.243860'
# date_time_obj = datetime.datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S.%f')

# print(date_time_str)
# print(date_time_obj)
