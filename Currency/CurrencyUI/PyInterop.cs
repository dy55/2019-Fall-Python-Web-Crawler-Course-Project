using System;
using System.IO;
using System.Diagnostics;
using System.Text;

namespace UIKit {
	interface IPythonInteropProcess {
		string Start(string commands, bool showShellWindow);
	}

	interface ICurrencyHubInterface {
		string Start(string cmds);
	}

	public class PythonInteropProcess : IPythonInteropProcess {
		public string Start(string commands, bool showShellWindow = false) {
			Process proc = new Process();
			ProcessStartInfo psi = new ProcessStartInfo("python", commands) {
				RedirectStandardOutput = true,
				CreateNoWindow = !showShellWindow,
				UseShellExecute = false
			};
			proc.StartInfo = psi;
			proc.Start();
			string result = proc.StandardOutput.ReadToEnd();
			proc.WaitForExit();
			return result;
		}
	}

	public class CurrencyHubInterface : ICurrencyHubInterface {
		public string Start(string cmds) {
			PythonInteropProcess piProc = new PythonInteropProcess();
			return piProc.Start($@"..\scripts\Hub.py {cmds}");
		}
	}

	public abstract class PyInteropUtils {
		private static CurrencyHubInterface cui = new CurrencyHubInterface();

		public static void VisualStat() {
			cui.Start("visualstat");
		}

		public static void VisualTrend(string from) {
			cui.Start("visualtrend " + from.ToLower());
		}

		public static void ExchangeRateCalc(string from, string to, out string[] outs) {
			outs = cui.Start($"rate {from} {to}").Split('\n');
		}

		public static string ExchangeRateCalc(string from, string to) {
			return cui.Start($"rate {from} {to}");
		}

		public static void ExchangeRateCalc<TIn>(string from, string to, TIn amount, out string[] outs) {
			outs = cui.Start($"rate {from} {to} {amount.ToString()}").Split('\n');
		}
	}
}
