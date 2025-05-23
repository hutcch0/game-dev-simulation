Version v0.5.0


🎮 Game Dev Simulation – Features
Text-based simulation of running a game development studio.

Develop games of three sizes: small, medium, big.

Name your game and set a custom price for each release.

Fans system:

Earn fans from successful games; fans boost sales for future releases.

Lose fans if a game performs poorly.

Dynamic sales simulation:

Sales phase lasts 60 seconds, with a live graph showing buyer growth.

Price affects sales: lower price = more buyers; price over $150 = no buyers.

Fans increase the number of buyers, especially at higher prices.

Random events during sales:

Events like “featured on a website,” “streamer boost,” or “bug discovered” can spike or dip sales and fans.

Event messages are shown under the sales graph.

Live timer below the sales graph shows how much sales time is left.

Money, days, and fans are tracked and shown at the bottom of the screen.

Simple, clean UI with clear prompts and feedback.

🕹️ Commands
Command	What it does

develop small	Start developing a small game (then name it and set a price)

develop medium	Start developing a medium game (then name it and set a price)

develop big	Start developing a big game (then name it and set a price)

status	Show your current money, days, and fans

help	Show the list of available commands

quit	Exit the game

During development:

You’ll be prompted to enter a game name and then a price (within a suggested range).

💡 How the Simulation Works
Development:

Choose size, name, and price for your game.

Development takes real time (30/60/120 seconds depending on size).

Sales:

Sales phase lasts 60 seconds, with buyers added every 10 seconds.

The price you set and your fans both affect how many people buy.

Random events can boost or reduce sales and fans.

If you set the price over $150, the game will not sell any copies.

At the end of the sales phase, your profit is buyers × price.

Successful games gain you more fans; flops may lose you fans.

📊 UI Overview
Main message area: Top left, always shows the latest prompt or event.

Sales graph: Right side, shows buyers over time during sales.

Timer: Below the sales graph, shows seconds left in the sales phase.

Event messages: Briefly appear under the graph during sales.

Status bar: Bottom right, shows money, days, and fans.

Input bar: Bottom left, for commands and prompts.
