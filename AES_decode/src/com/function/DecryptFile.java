package com.function;

import java.util.ArrayList;

//import com.main.GetName;
import com.utils.AES256;
import com.utils.GetLicenseTime;
import com.utils.ProcessStr;
import com.utils.RWfile;

public class DecryptFile {

	public static String decode(String decryptfilepath, String filename, String decryptcontent, String password)
			throws Exception {
		String decryptResult = AES256.decrypt(decryptcontent, password);
		return decryptResult;
	}

	public static String deSourceCode(String decryptFolder, String mac, String name,String licensePath) throws Exception {
		String decryptcontent = RWfile.Readpwd(name);
		String pwd = getPassword(licensePath,mac);
		String decode = decode(decryptFolder, name, decryptcontent, pwd);
		String[] str1 = decode.split("\r\n");
		String[] str2 = str1[1].split("#");
		String decontent = str2[0].substring(0, str2[0].length());
		String[] str3 = str1[0].split(" ");
		String time = str3[1] + str3[2];
		String newtime = time.replace(" ", "");
		newtime = newtime.replace("-", "");
		newtime = newtime.replace(":", "");
		String password = newtime;
		String result = decode(decryptFolder, name, decontent, password);
		return result;
	}

	public static String[] GetLicenseTime(String decryptFolder, String mac, String filename,String licensePath) throws Exception {
		String[] time = new String[4];
		String decryptcontent = RWfile.Readpwd(filename);
		String pwd = getPassword(licensePath,mac);
		String decode = decode(decryptFolder, filename, decryptcontent, pwd);
		String[] str1 = decode.split("\r\n");
		String[] str2 = str1[1].split("#");
		String[] str3 = str2[str2.length - 1].split(" ");
		time[0] = str3[0];
		time[1] = str3[1];
		time[2] = str3[2];
		String[] str4 = str1[0].split(" ");
		String date = str4[1];
		String currentTime = GetLicenseTime.getCurrentDate("yyyy-MM-dd");
		int day = GetLicenseTime.compareDate(date, currentTime, 0);
		time[3] = Integer.toString(day);
		return time;
	}

	public static boolean encryptSuccess(String folder, String mac,String licensePath) throws Exception {
		boolean b = false;

		String filename = "/pwd.txt";
		String decryptcontent = RWfile.Readpwd(filename);
//		String filename="ServerCall.py";
//		String decryptcontent=RWfile.Read(folder+"/"+filename);
		String password = getPassword(licensePath,mac);
		String str1 = decode(folder, filename, decryptcontent, password);
		if (str1 != null && str1.startsWith("#Foxconn")) {
			b = true;
		}
		return b;
	}
	
	public static String getPassword(String licensePath,String mac) {
		String validateCode=RWfile.ReadValidateCode(licensePath, mac);
		ArrayList<Integer> list=ProcessStr.getNumArray(validateCode);
		String password="";
		for(int i=0;i<list.size();i++) {
			password+=list.get(i);
		}
		String filepassword=AES256.encrypt(validateCode, password);
		return filepassword;
	}
}
