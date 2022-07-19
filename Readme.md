
# Selenium project that goes to a website and uploads csv files

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

```sh
git clone https://arulrajesh@dev.azure.com/arulrajesh/Harri%20Automation/_git/Harri%20Automation
```

### Initial setup. Skip to [ <a href="#reg">Steps for regular use </a>] if you have done initial setup.

1. Install a Virtualenv 

    ```sh
    pip install virtualenv
    ```

1. Pull the latest changes from the remote repository.

    ```sh
    git pull
    ```

1. Create a virtual environment called 'venv'.

    ```sh
    virtualenv venv
    ```

1. Activate the virtual environment.

    ```sh
    source venv/Scripts/activate
    ```

1. Install the dependencies.

    ```sh
    pip install -r requirements.txt
    ```

### Steps for regular use <div id='reg'></div>

1. > Edit the main.py to update the username, password and the URL line.
1. > Make sure there is folder called 'historicals' and it contains all the files that are to be uploaded for the above username.
1. > Make sure there is folder called 'logs'. The logs generated while the script is running are stored here.

1. > *Open a new git bash prompt and enter the following commands.*


    1. Activate the virtual environment.
        - git bash
            ```sh
            source venv/Scripts/activate
            ```
        <div align = center> OR </div>
        
        - on windows cmd
            ```sh
            harri\Scripts\activate.bat
            ```

    1. Run the createlist program to create 'list.csv'.

        ```sh
        python main.py createlist
        ```

    1. > Verify the 'list.csv' file and make sure there are no zzzzzz, otherwise give the correct clientID. The clientID is the search term that used to search for
        the brand. It should result in only one result to avoid ambiguity.

    1. Run the upload script

        ```sh
        python main.py upload
        ```
