# slack-use
Small programs to get and send messages to and from slack.

# Execution
```
  python3 loop_getter.py &
```
- When you want to stop, kill this process.(e.g. kill %1)

# As a result
- Newly updated information on slack are written files under logs/
- And also, send to local syslog file.

# Others
- .latest_ts_record.log record the latest record TimeStamp, so if you'd like to re-import, remove this file before execution.
