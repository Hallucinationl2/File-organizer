by using pyinstaller you can make the scirpt into .exe file
1. step: open cmd
2. cd <desktop file organizer path>
3. after you changed the cd to the correct path copy pasta the code down and change paths
4. pyinstaller --noconfirm --onedir --windowed --add-data "<CustomTkinter Location>/customtkinter;customtkinter/"  "<Path to Python Script>"
