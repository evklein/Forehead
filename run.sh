#!/bin/bash

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