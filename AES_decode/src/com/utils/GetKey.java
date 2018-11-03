package com.utils;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.UUID;

public class GetKey {

	public static String getLastModifiedTime(String filepath) {
		File file = new File(filepath);
		long time = file.lastModified();
		String ctime = new SimpleDateFormat("yyyyMMddHHmmss").format(new Date(time));
		return ctime;
	}

	public static String getGUID() {
		UUID uuid = UUID.randomUUID();
		String a = uuid.toString();
		a = a.toUpperCase();
		return a;
	}

	public static String getMac() {
		String mac = "";
		String os = System.getProperty("os.name");
		if (os.toLowerCase().startsWith("win")) {
			try {
				mac = getMacByWindows();
			} catch (IOException e) {
				e.printStackTrace();
			}
		} else {
			mac = getMacByLinux();
		}
		mac = mac.toUpperCase();
		return mac;
	}

	private static String getMacByWindows() throws IOException {
		String result = "";
		Process process = Runtime.getRuntime().exec("ipconfig /all");
		BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream(), "GBK"));

		String line;
		int index = -1;
		while ((line = br.readLine()) != null) {
			index = line.toLowerCase().indexOf("physical address");
			if (index >= 0) {
				index = line.indexOf(":");
				if (index >= 0) {
					result = line.substring(index + 1).trim();
				}
				break;
			}
		}
		br.close();
		result = result.replace(":", "");
		result = result.replace("-", "");
		return result.toUpperCase();
	}

	@SuppressWarnings("static-access")
	private static String getMacByLinux() {
		StringBuffer sb = new StringBuffer();
		try {
			for (int i = 0; i < 50; i++) {
				String str = "cat /sys/class/net/*/address | sed -n '" + i + "p'";
				String[] cmd = new String[] { "/bin/sh", "-c", str };
				Process process = Runtime.getRuntime().exec(cmd);
				BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream()));
				String line;
				while ((line = br.readLine()) != null) {
					sb.append(line);
				}

			}
		} catch (IOException e) {
			e.printStackTrace();
		}

		String s = sb.toString().toUpperCase();
		s = s.replace(":", "");
		s = s.replace("-", "");

		String[] list = new String[s.length() / 12];
		int sl = s.length();
		for (int i = 0; i <= sl; i++) {
			if (i % 12 == 0 && i != 0) {
				int set = i / 12 - 1;
				String s2 = s.substring(set * 12, i);
				list[set] = s2;
			}
		}

		String macs = "".join(",", list);
		return macs;
	}

//	public static void main(String[] args) {
//		String mac = getMac();
//		System.out.println(mac);
//	}
}
