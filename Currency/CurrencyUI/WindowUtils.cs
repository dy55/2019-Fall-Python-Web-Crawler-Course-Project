using System;
using System.Collections.Generic;
using System.Text;
using System.Windows;

using CurrencyUI;

namespace UIKit {
	public static class WindowUtils {
		public static void ShowException(Exception e) {
			MessageBox.Show(e.ToString(), "程序发生异常", MessageBoxButton.OK, MessageBoxImage.Error);
		}
	}
}
