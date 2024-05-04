How to run :

Edit Server1.py file in 'main' to run the server on desired port as follows:

if __name__ == '__main__':
    # start_server()
    app.run(host='localhost', port=DESIRED_PORT, debug=True)

Then follow below steps:

Step 1:
Open the terminal, and navigate to the location of the file 'Server1.py' and run:
cmd: "python Server1.py"

PS: Remeber to start the server before client and close the server before client.

Step 2:
Open Streamlit folder in terminal and run the following commands in different terminal window:

"Streamlit run frontend.py"
"python app.py"
