# Stations

A series of bash scripts and systemd services/timers that allow the public computers to close themselves down at a certain time.

## Usage

* `station close <user name>` closes the station loggin out the supplied user in the process.
* `station open <user name>` opens the station.
* `station setup <user name>` enables and starts all required systemd timers.  Do this when you're ready for the stations to begin closing themeselves.
* `station teardown <user name>` disables and stops all required systemd timers.  Do this when you'd like the stations to not close automatically.   

## Setting up timers

Timers are based upon the `OnCalendar=` directives.

Shutdown timers are setup to fire 10 minutes before the library closes.  They are set to fire every 15 seconds between computer shutdown time and library closing time.

__Example of closing timing__

```
[Timer]
OnCalendar=Mon..Thu 17:45..59:0/15
OnCalendar=Fri..Sat 16:45..59:0/15
AccuracySec=1s
```

Notification timers should be set up to run 10 minutes before the station-close timer fires.  They are currently setup to run 1/minute until 1 minute before shutdown.

__Example of notification timing__

```
[Timer]
OnCalendar=Mon..Thu 17:40..49/1
OnCalendar=Fri..Sat 15:40..49/1
AccuracySec=1s
```

Open timers are set up to fire 30 minutes after closing.  They are also set to be persistent. So, if the computer is shut down at the time it is supposed to open itself, it will fire the open service as soon as it boots.


__Example of opening timing__

```
[Timer]
OnCalendar=Mon..Thu 18:30
OnCalendar=Fri..Sat 17:30
Persistent=true
AccuracySec=1s
```

