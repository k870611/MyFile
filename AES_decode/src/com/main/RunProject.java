package com.main;

import java.util.ArrayList;
import java.util.Properties;

import org.python.util.PythonInterpreter;

import com.function.DecryptFile;
import com.utils.GetKey;
import com.utils.RWfile;

public class RunProject {

	public static void main(String[] args) {

		String jar_name = GetName.GiveMeName();
		String folder = System.getProperty("user.dir");
		String licensePath = System.getProperty("user.dir")+"/License.txt";
//		String folder="C:\\Users\\H7109225\\Desktop\\AES\\user\\E8-39-35-2C-AA-45\\ServerCall_20181011_1041";
//		String licensePath = "C:\\Users\\H7109225\\Desktop\\AES\\user\\E8-39-35-2C-AA-45\\ServerCall_20181011_1041"+"/License.txt";

		
		String localMac = GetKey.getMac();
		String[] macs = localMac.split(",");
		try {
			for (int j = 0; j < macs.length; j++) {
				String mac = macs[j];
				boolean b = DecryptFile.encryptSuccess(folder, mac,licensePath);
				String filemac=RWfile.ReadMac(licensePath);
				if (b == true && mac.equals(filemac)) {
					String[] time = new String[4];
					String filename = "/pwd.txt";
					time = DecryptFile.GetLicenseTime(folder, mac, filename,licensePath);

					int licenseTotalTime = Integer.parseInt(time[0]);
					int licenseWarningTime = Integer.parseInt(time[1]);
					int licenseSecondWarningTime = Integer.parseInt(time[2]);
					int day = Integer.parseInt(time[3]);

					if (day >= 0) {

						if (day > licenseTotalTime) {
							System.out.println("File " + jar_name + " license is expired!");
						} else {
							int num = licenseTotalTime - day;
							if (day > (licenseTotalTime - licenseSecondWarningTime) && day <= licenseTotalTime) {
								System.out.println("Serious Warning!!! " + "File " + jar_name
										+ " license will expire in " + num + " days");
							}
							if (day > (licenseTotalTime - licenseSecondWarningTime - licenseWarningTime)
									&& day <= (licenseTotalTime - licenseSecondWarningTime)) {
								System.out.println(
										"Warning! " + "File " + jar_name + " license will expire in " + num + " days");
							}

							Properties props = new Properties();
							props.put("python.console.encoding", "UTF-8");
							props.put("python.security.respectJavaAccessibility", "false");
							props.put("python.import.site", "false");
							Properties preprops = System.getProperties();
							PythonInterpreter.initialize(preprops, props, new String[0]);
							PythonInterpreter interpreter = new PythonInterpreter();
							interpreter.exec("import sys");
							String jythonPath = folder + "/lib/jythonLib";
							String jythonPath1 = "sys.path.append('" + jythonPath + "')";
							String jythonPath2 = "sys.path.append('" + jythonPath + "/site-packages')";
							interpreter.exec(jythonPath1);
							interpreter.exec(jythonPath2);

							String header = "";
							String decryptResult = DecryptFile.deSourceCode(folder, mac, filename,licensePath);
							ArrayList<String> list = new ArrayList<String>();
							for (int i = 0; i < args.length; i++) {
								list.add("'" + args[i] + "'");
							}
							String version = GetName.GiveMeVersion();
							list.add("'" + version + "'");
							
							header = "arg=" + list.toString();
							decryptResult = header + "\r\n" + decryptResult;
							interpreter.exec(decryptResult);
							interpreter.close();
						}

					} else {
						System.out.println("System time error!");
					}

					break;

				} else if (!b && j == macs.length - 1) {
					System.out.println("It cannot run because incorrect information!");
				}

			}

		} catch (Exception e) {

		}

	}
}