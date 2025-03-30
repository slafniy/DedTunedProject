set project=DedTuned
set toolkit_path="D:\SteamLibrary\steamapps\common\Baldurs Gate 3 Toolkit\"
set lsx2lsf="C:\Users\slafniy\Desktop\bg3modding\bg3lsx2lsf\bg3lsx2lsf.exe"
set lsx_input_dir=%~dp0LSX_RootTemplates
set lsf_output_dir=%~dp0Public/DedTuned_de9f3db5-7ca9-a872-75d4-3cc4a09a90cd/RootTemplates

::convert LSX root templates
%lsx2lsf% %lsx_input_dir% %lsf_output_dir%

cd /D %toolkit_path%

::%toolkit_path%\Glasses.exe -project %project% -lvl WLD_Main_A
%toolkit_path%\Glasses.exe -project %project% -lvl Basic_Level_A