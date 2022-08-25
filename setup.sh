mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml

echo "\
[CONFIG_KEY]\n\
apiKey = 'AIzaSyA5ylnqAg64aMqPixVvh0JXABvI1tizeVk'\n\
authDomain = 'prodesex-8e59f.firebaseapp.com'\n\
databaseURL = 'https://prodesex-8e59f-default-rtdb.firebaseio.com'\n\
projectId = 'prodesex-8e59f'\n\
storageBucket = 'prodesex-8e59f.appspot.com'\n\
messagingSenderId = '191772777462'\n\
appId = '1:191772777462:web:cb327de1c21875275685d7'\n\
measurementId = 'G-Z576SW3PKH'\n\
\n\
" > ~/.streamlit/secrets.toml