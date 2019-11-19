using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.IO;
using System.Threading;
using System.Text.RegularExpressions;

using Newtonsoft.Json;

using UIKit;

namespace CurrencyUI {
	/// <summary>
	/// Interaction logic for MainWindow.xaml
	/// </summary>
	public partial class MainWindow : Window {
		/// <summary>
		/// Fields of MainWindow class
		/// </summary>
		protected Dictionary<string, string> CurrencyList { get; private set; }
		private string previousText;

		public MainWindow() {
			InitializeComponent();
			Initialize();
			StatusBlock.Content = "就绪";
		}

		private void Initialize() {
			Uri statIconUri = new Uri(@"..\icons\exchange.ico", UriKind.RelativeOrAbsolute);
			Icon = BitmapFrame.Create(statIconUri);

			CurrencyList = JsonConvert.DeserializeObject<Dictionary<string, string>>(File.ReadAllText(@"..\data\currencyShort.json"));

			foreach(var i in CurrencyList) {
				ComboBoxItem item1 = new ComboBoxItem();
				ComboBoxItem item2 = new ComboBoxItem();
				item1.Content = i.Key;
				item2.Content = i.Key;
				fromCombo.Items.Add(item1);
				toCombo.Items.Add(item2);
			}
			fromCombo.SelectedIndex = 0;
			toCombo.SelectedIndex = 0;

			previousText = fromBox.Text;

			fromExEng.Content = CurrencyList[fromCombo.Text];
			toExEng.Content = CurrencyList[toCombo.Text];
		}

		private void Close_Click(object sender, RoutedEventArgs e) {
			Close();
		}

		private void AboutItem_Click(object sender, RoutedEventArgs e) {
			AboutWindow about = new AboutWindow();
			about.Visibility = Visibility.Visible;
		}

		private void StatView_Click(object sender, RoutedEventArgs e) {
			StatusBlock.Content = "正在执行操作";
			SetEvent("正在运行", isIndeterminate: true);
			LoadingWindow LoadingWindow = new LoadingWindow();
			LoadingWindow.Visibility = Visibility.Visible;
			Thread mainOpThread = new Thread(() => {
				try {
					PyInteropUtils.VisualStat();
				}
				catch(Exception e) {
					WindowUtils.ShowException(e);
				}
				Dispatcher.BeginInvoke(new Action(() => {
					DisposeEvent();
					StatusBlock.Content = "就绪";
					LoadingWindow.Close();
				}));
			});
			mainOpThread.Start();
		}

		private void StatTrend_Click(object sender, RoutedEventArgs e) {
			if (fromCombo.Text.Equals("人民币")) {
				MessageBox.Show("无法查询 人民币 -> 人民币的汇率趋势", "错误", MessageBoxButton.OK, MessageBoxImage.Error);
				return;
			}
			if (MessageBox.Show($"确定要查询 {fromCombo.Text} -> 人民币的汇率趋势？", "确认", MessageBoxButton.YesNo, MessageBoxImage.Question) == MessageBoxResult.No)
				return;
			StatusBlock.Content = "正在执行操作";
			LoadingWindow loadingWindow = new LoadingWindow();
			loadingWindow.Visibility = Visibility.Visible;
			SetEvent("正在运行", isIndeterminate: true);
			Thread mainOpThread = new Thread(() => {
				string targetEx = new string("");
				Dispatcher.Invoke(() => {
					targetEx = CurrencyList[fromCombo.Text];
				});
				PyInteropUtils.VisualTrend(targetEx);
				Dispatcher.BeginInvoke(new Action(() => {
					DisposeEvent();
					StatusBlock.Content = "就绪";
					loadingWindow.Close();
				}));
			});
			mainOpThread.Start();
		}

		private void HelpItem_Click(object sender, RoutedEventArgs e) {
			HelpWindow hw = new HelpWindow();
			hw.Visibility = Visibility.Visible;
		}

		void ShowExchangeContent(string from, string to, decimal rate) {
			ExchangeLbl.Content = $"1 {from} = {rate:G16} {to}";
		}

		private void SearchBtn_Click(object sender, RoutedEventArgs e) {
			if (fromBox.Text.Equals("")) {
				toBox.Text = "";
				MessageBox.Show("没有输入数值", "警告", MessageBoxButton.OK, MessageBoxImage.Warning);
				return;
			}
			StatusBlock.Content = "正在查询";
			SetEvent("正在运行", isIndeterminate: true);
			fromCombo.IsEnabled = false;
			fromBox.IsEnabled = false;
			toCombo.IsEnabled = false;
			SearchBtn.IsEnabled = false;
			Thread opThread = new Thread(() => {
				string[] results = new string[3];
				try {
					string fromEx = new string("");
					string toEx = new string("");
					decimal amount = new decimal();
					Dispatcher.Invoke(new Action(() => {
						fromEx = CurrencyList[fromCombo.Text];
						toEx = CurrencyList[toCombo.Text];
						amount = Convert.ToDecimal(fromBox.Text);
					}));
					PyInteropUtils.ExchangeRateCalc(fromEx, toEx, amount, out results);
					Dispatcher.Invoke(new Action(() => {
						toBox.Text = $"{Convert.ToDecimal(results[0]):G16}";
						ShowExchangeContent(fromCombo.Text, toCombo.Text, Convert.ToDecimal(results[1].Split(' ')[3]));
					}));
				}
				catch (Exception ex) {
					WindowUtils.ShowException(ex);
				}
				Dispatcher.BeginInvoke(new Action(() => {
					StatusBlock.Content = "就绪";
					fromCombo.IsEnabled = true;
					fromBox.IsEnabled = true;
					toCombo.IsEnabled = true;
					SearchBtn.IsEnabled = true;
					DisposeEvent();
				}));
			});
			opThread.Start();
		}

		private void ExchangeLbl_Loaded(object sender, RoutedEventArgs e) {
			
		}

		private void FromBox_TextChanged(object sender, TextChangedEventArgs e) {
			if (new Regex(@"^(\d?|[1-9]\d+(\.\d*)?|\d\.\d*)$").Match(fromBox.Text).Success)
				previousText = fromBox.Text;
			else {
				fromBox.Text = previousText;
				fromBox.Select(fromBox.Text.Length, 0);
			}
		}

		private void fromCombo_SelectionChanged(object sender, SelectionChangedEventArgs e) {
			fromExEng.Content = CurrencyList[(e.AddedItems[0] as ComboBoxItem).Content as string];
		}

		private void toCombo_SelectionChanged(object sender, SelectionChangedEventArgs e) {
			toExEng.Content = CurrencyList[(e.AddedItems[0] as ComboBoxItem).Content as string];
		}
		
		public void SetEvent(string eName, double progress = 0, double minValue = 0, double maxValue = 100, bool isIndeterminate = false) {
			EventBlock.Visibility = Visibility.Visible;
			EventProgress.IsIndeterminate = isIndeterminate;
			if (!isIndeterminate) {
				EventProgress.Minimum = minValue;
				EventProgress.Maximum = maxValue;
				EventProgress.Value = progress;
			}
			EventName.Content = eName;
		}

		public void UpdateEventProgress(double progress = 0, bool isIndeterminate = false) {
			EventProgress.IsIndeterminate = isIndeterminate;
			if (!isIndeterminate)
				EventProgress.Value = progress;
		}

		public void DisposeEvent() {
			EventBlock.Visibility = Visibility.Hidden;
			EventProgress.Value = 0;
			EventProgress.IsIndeterminate = false;
			EventName.Content = "";
		}
	}
}
