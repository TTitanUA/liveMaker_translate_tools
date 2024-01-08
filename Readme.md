This is an automatic translation, may be incorrect in some places.

# LiveMaker Translation Tools
## Description
This application includes a set of tools for translating games powered by the LiveMaker engine.
It supports both fully automatic translation (Azure AI Translator) and manual translation (Tolgee or any other service that can work with localization JSON files in i18n format).

Built upon:
- [pylivemaker](https://github.com/pmrowla/pylivemaker/tree/master)
- [pylivemaker-tools](https://github.com/Stefan311/pylivemaker-tools)

**HUGE RESPECT to the authors!!!**

## Usage
This is the first version of the application, so it does not contain a graphical user interface.
To use it, you need to run the `main.py` file using Python 3.11+.
The application will work in console mode.

### Project Preparation
1. Create a `project` folder at the root of the application.
2. Inside it, create a folder with the name of your project (for instance, `my_project`).
3. In the project folder create a `game` folder and place the game files into it.
4. In the `main.py` file, specify the name of your project in the `project_name` variable.
5. In the `main.py` file, specify the name of the main game file in the `main_file` variable, e.g., `game.exe`.
This might not necessarily be an EXE file, but rather the file containing the resource archive. (Tested only on EXE file).

### Resource Extraction
1. Open the `main.py` file and change the `stage` variable value to `extract`.
2. Run the `main.py` file.
3. If everything is successful, the `extract` folder with unpacked resources and the `translate` folder with `*.csv` and `origin.json` will appear in the `project` folder.

### Translation
#### Automatic Translation (not mandatory)
Azure AI Translator service is used for automatic translation.
Firstly, you have to sign up for an account on [Azure](https://portal.azure.com/) – you get 2,000,000 characters per month for free.
After registering, you need to create a resource for the translator.
Once the resource is created, you need to obtain the access key to it.
For this, go to the resource settings and in the "Keys and Endpoints" section, copy the value of the access key.
1. Copy the `config.example.py` file to `config.py` and paste the access key, endpoint, and region into it.
2. Open the `main.py` file and change the `stage` variable value to `translate`.
3. Run the `main.py` file. And go drink tea, coffee, or whatever you like.
4. A file `translate.json` with the translated strings will appear in the `translate` folder. Also, a `cache` folder with a cache of translated strings will appear in the `project` folder (to avoid unnecessary API usage).
5. If you don't like the translation, you can manually edit the `translate.json` file.

#### Manual Translation
For manual translation, any service that can work with i18n format JSON localization files (a regular dictionary) can be used.
The original localization file can be found in the `translate` folder and is named `origin.json`.
It is advisable not to feed the entire translation file to the service, but rather extract only unique strings. In the games I've come across, there were quite a lot of repetitions.
Save the translation results in the `translate.json` file in the `translate` folder.

#### Updating CSV
1. Open the `main.py` file and change the `stage` variable value to `insert`.
2. Run the `main.py` file.
3. The `*.csv` files in the `translate` folder will be updated with a new column containing the translation.

### Patching
Make sure there is no `result` folder in the project folder; if it exists, delete it.
1. Open the `main.py` file and change the `stage` variable value to `patch`.
2. Run the `main.py` file.
3. A `result` folder with patched game resources will appear in the `project` folder.
4. Open the `main.py` file and change the `stage` variable value to `none`.
5. Go to the `result` folder and launch the game.

## TODO
- [ ] Add a graphical user interface
- [ ] Add the ability to translate menu strings (currently disabled as it breaks the game)
- [ ] Add utilities to assist in manual translation

## Bugs and feedback
If you find bugs, create [issue](https://github.com/TTitanUA/liveMaker_translate_tools/issues)
The library is open for further development and your [pull requests](https://github.com/TTitanUA/liveMaker_translate_tools/pulls)!
