# Tracker

Convenient terminal application to store and keep track of any numeric values.

## Installation

Tracker can be installed from test PyPI using a little bit customized `pip` command:

```
pip3 install --upgrade -i https://test.pypi.org/simple/ --extra-index-url https://pypi.python.org/simple tracker
```

You can take advantage of the autocompletion too, set in your .bashrc/.zshrc/.profile/whatever

```
eval "$(register-python-argcomplete3 tracker)"
```

## Usage

### CLI

Add a few keys/entries

```console
$ tracker abc.key1 2
Measure added
 ┌──────────────────────────────────────────────────────────────────────┐
3┤                                                                      │
 │                                                                      │
 │                                                                      │
 │                                                                      │
 │                                                                      │
 │                                                                      │
 │                                                                      │
 │                                                                      │
 │                                                                      │
2┤                                                                     •│
 │                                                                      │
 │                                                                      │
 │                                                                      │
 │                                                                      │
 │                                                                      │
 │                                                                      │
 │                                                                      │
 │                                                                      │
1┤                                                                      │
 └┬───────────┬─────────┬─────────┬─────────┬─────────┬─────────┬──────┬┘
12/05       14/05     15/05     16/05     17/05     18/05     19/05 19/05
$ tracker abc.key1 1 --date 2021-05-13
Measure added
   ┌────────────────────────────────────────────────────────────────────┐
  2┤                                                                   •│
   │                                                                ••• │
   │                                                            ••••    │
   │                                                         •••        │
   │                                                     ••••           │
   │                                                 ••••               │
   │                                              •••                   │
   │                                          ••••                      │
   │                                       •••                          │
1.5┤                                   ••••                             │
   │                               ••••                                 │
   │                            •••                                     │
   │                        ••••                                        │
   │                     •••                                            │
   │                 ••••                                               │
   │             ••••                                                   │
   │          •••                                                       │
   │      ••••                                                          │
  1┤  ••••                                                              │
   └┬───────────┬────────┬─────────┬─────────┬─────────┬────────┬──────┬┘
  12/05       14/05    15/05     16/05     17/05     18/05    19/05 19/05
```

You could also increment an existing measure

```console
tracker abc.key1 --incr --date 2021-05-13
Measure incremented to 2
   ┌────────────────────────────────────────────────────────────────────┐
  2┤  ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••│
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
1.5┤                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
  1┤                                                                    │
   └┬───────────┬────────┬─────────┬─────────┬─────────┬────────┬──────┬┘
  12/05       14/05    15/05     16/05     17/05     18/05    19/05 19/05
```

Create a key without any measures

```console
$ tracker bcd.key1 --empty
Empty key created
```

Show the existing keys

```console
$ tracker     
--------
abc.key1
abc.key2
bcd.key1
--------
```

Show a subset of keys

```console
$ tracker abc.
--------  --
abc.key1   1
abc.key2   3
--------  --
```

Show the raw measures data

```console
$ tracker abc.key1 --raw 
2021-05-13 00:00:00 1620856800 2
2021-05-19 17:45:26 1621439126 2
2021-12-05 00:00:00 1638658800 1
```

Delete a key

```console
$ tracker abc.key2 --delete
Are you sure to delete <Key: abc.key2> ? [y/N] y
```

Show the existing measures for the last 7 days

```console
$ tracker abc.key1         
   ┌────────────────────────────────────────────────────────────────────┐
  2┤  ••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••••│
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
1.5┤                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
   │                                                                    │
  1┤                                                                    │
   └┬───────────┬────────┬─────────┬─────────┬────────┬─────────┬──────┬┘
  12/05       14/05    15/05     16/05     17/05    18/05     19/05 19/05
```
