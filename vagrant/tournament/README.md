# Swiss Tournament PostgreSQL Database:

This project employs SQL and Python 2.7 to create and manage a database for running a "Swiss-system" tournament, a description of which can be found [here](https://en.wikipedia.org/wiki/Swiss-system_tournament).

## Quick(ish)start

### Setting up The Database:

#### Step 1:
 In order to run use this code, a virtual machine is required, and psql (PostgreSQL) must be installed. The recommended way to do this is to install VirtualBox amd Vagrant.
VirtualBox can be downloaded [here](https://www.virtualbox.org/wiki/Downloads), and Vagrant from [here](https://www.vagrantup.com/downloads.html) choosing the correct version for your operating system. It is not yet necessary to initialise Vagrant in any particular directory.

#### Step 2:
Secondly you must clone this repository to your own computer using git.

#### Step 3:
Thirdly, navigate to the directory containing the clone in your command line and enter the vagrant directory like this:
```cd <your/entire/file/pathway/vagrant>```

#### Step 4:
Initialise vagrant by typing `vagrant up`. This starts up vagrant, but the first time it is run in a particular directory, it will also create the virtual machine. A file is included so that vagrant is configured properly.

#### Step 5:
After the extended process of downloading an entire Linux operating system, if you are using Windows you will need to change to using a Linux Bash shell rather than the inbuilt Command Prompt. Happily you already have one installed in the guise of Git Bash. Open your Bash shell, navigate again into the cloned repository (again using `cd <your/entire/file/pathway/vagrant>`), and enter into the virtual machine via `vagrant ssh`.

#### Step 6:
Ensure that you are in `/vagrant/tournament`, and start PostgreSQL by typing `psql`

#### Step 7:
Make a new database called tournament (not anything else, or the functions written here will not work) by typing `CREATE DATABASE tournament;`, then enter into it by typing `\c tournament`.

#### Step 8:
import tournament.sql via `\i tournament.sql`. This will set up your database tables and views so they can be used by the given functions.

### Using the functions to run a Swiss Tournament:

All functions are contained within the tournament.py file. Recommended use is through importing that file into a Python 2.7 document, either via `from tournament import *`, or simply `import tournament` if you wish to preserve similar names for future use within your program.

For the initial tournament, it won't be necessary to run `deleteMatches()` or `deletePlayers()` but because the database is set up to manage only one tournament at a time, you'll need to run them as the first step for any subsequent tournament.

Next step will be entering each of the contestants into the database. To do so, simply run `registerPlayer('Full Name')` for each player. This database only supports an even number of players, so ensure that this is the case before continuing.

Once all players have been entered, running `swissPairings()` for the first time will give you your sets of pairings for the initial round.

The result of each game can be entered into the database by running reportMatch(winner_ID, loser_ID). Your original `swissPairings()` result contains the IDs, or you can also obtain each player ID from the database by typing into psql:

```SELECT id FROM players WHERE name='player's name';```

Once all match results for the round have been entered, the next set of pairings can be determined by running `swissPairings()` again.

The number of rounds required in a swiss tournament is determined by log<sub>2</sub>(players/2) where players here is rounded up to a power of 2, so:

4 players: 2 rounds
8 players: 3 rounds
16 players: 4 rounds
32 players: 5 rounds

and so on.

After so many rounds are played, the resulting standings list is your final tournament result. This can be retrieved by running `playerStandings()`.

## Contributions

The guidelines for this project were written by Udacity and presented by course developer Karl Krueger as part of the Full Stack Web Developer Nanodegree. SQL and Python in this project were written by Siobhan Hokin.

## Licence

In so far as any code is copyright Siobhan Hokin, it is published under the MIT license which can be read [here](https://opensource.org/licenses/MIT). All else is copyright Udacity.




