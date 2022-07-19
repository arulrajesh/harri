
# Selenium project that goes to a website and uploads csv files

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

```sh
git clone https://arulrajesh@dev.azure.com/arulrajesh/Harri%20Automation/_git/Harri%20Automation
```

### First time setup

1. Install a Virtualenv skip to (<a href="#reg">Steps for regular use </a>) if you have done initial setup.

    ```sh
    pip install virtualenv
    ```

1. Pull the latest changes from the remote repository.

    ```sh
    git pull
    ```

1. Create a virtualenvironment called 'venv' (to be run only once while setting up)

    ```sh
    virtualenv venv
    ```

1. Activate the virtual environment

    ```sh
    source venv/Scripts/activate
    ```

1. Install the dependencies

    ```sh
    pip install -r requirements.txt
    ```

### Steps for regular use <div id='reg'></div>

1. > Edit the main.py to update the username, password and the URL line.
1. > Make sure there is folder called 'historicals' and it contains all the files that are to be uploaded for the above username
1. > Make sure there is folder called 'logs'. The logs generated while the script is running are stored here

1. ### Open a new cmd prompt and enter the following commands.


    1. Activate the virtual environment

        ```sh
        source venv/Scripts/activate
        ```

    1. Run the createlist program to create 'list.csv'

        ```sh
        python main.py createlist
        ```

    1. > Verify the 'list.csv' file and make sure there are no zzzzzz, otherwise give the correct clientID. The clientID is the search term that used to search for
        the brand. It should result in only one result to avoid ambiguity.

    1. Run the upload script

        ```sh
        python main.py upload
        ```
