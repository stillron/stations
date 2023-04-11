# Stations

A series of bash scripts and systemd services/timers that allow the public computers to close themselves down at a certain time.

## Setting up timers

Timers are based upon the `OnCalendar=` directives.

Shutdown timers are setup to fire 10 minutes before the library closes.  They are set to fire every 15 seconds between computer shutdown time and library closing time.

__Example__

```
[Timer]
OnCalendar=Mon..Thu 17:45..59:0/15
OnCalendar=Fri..Sat 16:45..59:0/15
AccuracySec=1s
```

Notification timers should be set up to run 10 minutes before the station-close timer fires.  They are currently setup to run 1/minute until 1 minute before shutdown.

__Example__

```
[Timer]
OnCalendar=Mon..Thu 17:40..49/1
OnCalendar=Fri..Sat 15:40..49/1
AccuracySec=1s
```

