set project=DedTuned
set toolkit_path="D:\SteamLibrary\steamapps\common\Baldurs Gate 3 Toolkit\"
set lsx2lsf="C:\Users\slafniy\Desktop\bg3modding\bg3lsx2lsf\bg3lsx2lsf.exe"

set path_to_convert=%~dp0Public/DedTuned_de9f3db5-7ca9-a872-75d4-3cc4a09a90cd/RootTemplates

%lsx2lsf% %path_to_convert%

cd /D %toolkit_path%

::%toolkit_path%\Glasses.exe -project %project% -lvl WLD_Main_A
%toolkit_path%\Glasses.exe -project %project% -lvl Basic_Level_A