   M S B A M L   `   `   `  ���� E  ACurrencyUI, Version=1.0.0.0, Culture=neutral, PublicKeyToken=null'clr-namespace:CurrencyUI
CurrencyUI      CurrencyUI.MainWindow   \ XPresentationFramework, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35e aSystem.Windows.Controls.Ribbon, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089W SPresentationCore, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35R NWindowsBase, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35F 9http://schemas.microsoft.com/winfx/2006/xaml/presentation     R NSystem.Xaml, Version=4.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089:x,http://schemas.microsoft.com/winfx/2006/xaml     @d2http://schemas.microsoft.com/expression/blend/2008     Jmc;http://schemas.openxmlformats.org/markup-compatibility/2006     *localclr-namespace:CurrencyUI       � Title$!  汇率转换与统计工具��$	��450��$	��450��$*��$DengXian, Microsoft Yahei UI, 宋体)�.���    
gridStyle1#��[  .+�o�   
menuStyle1#��[ .@�m� $��
文件(_F)��  menuItemStyle#��[ .@�m� -    m�Name$ 	CloseItem��$��
关闭(_C)��m� $��
视图(_V)��#��[ .@�m� -   $��StatView��$��汇率概览(_B)��m� -   $��	StatTrend��$��汇率趋势(_T)��m� $��
关于(_A)��#��[ .@�m� -   $��HelpItem��$��
帮助(_H)��m� -   $ 	AboutItem��$��
关于(_A)���� $��123,100,123,29q�.+�]� .+��� -   $��	fromExEng��$�� ��$��Right=�$��40��  engNameLableStyle#��[ �� -   $��	fromCombo��  
comboStyle#��[ $
��Left=��� -   $��fromBox��$	��0 5q��� -	    ��Name$ reverse��$��Center=�$��Center=�$	��↓��$��50 30q�$��50��$��35(�$
��Bold"�
���"�"�]� .+��� -
   $��toExEng��$�� ��$��Right=�$��40��#��[ �� -   $��toCombo��#��[ $
��Left=��� -    ��Name$ toBox�� �� Padding$	 0 5q�
�������${�False���� -   $ ExchangeLbl��$�� ���� -   $��	SearchBtn��$��查询��$��Right=�  	btnStyle1#��[ ��   statusBarStyle1#��[ .@��� -    ��Name$ StatusBlock��$��正在初始化��$
��Left=�$	��120���� $��Right=�.��]� -   $��
EventBlock��$y�Hidden=�.+��� -   $��	EventName��$�� ��$��70��$��Center=�� -    �Name$ EventProgress��$	��100��$��12��