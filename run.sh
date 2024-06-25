#!/bin/bash

# Take a copy of the database
date=$(date '+%Y-%m-%d-%H_%M_%S')
cp api/db.sqlite3 backups/backup-$date.sqlite3

# Start the Svelte development server
cd svelte
npm run dev &
svelte_pid=$!

# Start the Django development server
cd ../api
python3 manage.py runserver &
django_pid=$!

# Wait for both processes to finish
wait $svelte_pid
wait $django_pid
