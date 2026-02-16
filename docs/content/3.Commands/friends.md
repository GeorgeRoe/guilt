---
title: Friends
description: Lists other GUILT users on the same HPC system
navigation:
  icon: i-lucide-user-search
---

## Usage

```bash [Terminal]
guilt friends
```

## Description

The GUILT `friends` command lists other GUILT users on the same HPC system.
This doesn't have a real use other than serving the users curiosity.

## How it works

::steps{level=4}
#### Get entries from the password database

GUILT queries the system's password database to retrieve a list of all user accounts on the HPC system:

```bash [Terminal]
getent passwd
```

It will parse the output of this command to extract the usernames and home directories of all users.

#### Check for GUILT usage

For each user retrieved from the password database, GUILT checks if they have a GUILT directory in their home directory.
If they do, they will be classed as a GUILT user.

#### Display the list of GUILT users

Finally, GUILT will list the users who have been identified as GUILT users to the terminal.
::