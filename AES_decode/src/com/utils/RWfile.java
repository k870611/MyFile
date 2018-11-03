package com.utils;

import java.io.File;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

public class RWfile {

	// read file
	public static String Read(String pathname) {

		String str = "";
		File file = new File(pathname);
		try {
			FileInputStream in = new FileInputStream(file);
			int size = in.available();
			byte[] buffer = new byte[size];
			in.read(buffer);
			in.close();
			str = new String(buffer, "UTF-8");
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}

		return str;
	}
	
	// read file
	public static String Readpwd(String pathname) {
		String str = "";

		try {
			Path temp = Files.createTempFile("resource-", ".ext");
			Files.copy(RWfile.class.getResourceAsStream(pathname), temp, StandardCopyOption.REPLACE_EXISTING);
			//FileInputStream in = new FileInputStream(file);
			FileInputStream in = new FileInputStream(temp.toFile());
			//InputStream in = RWfile.class.getResourceAsStream(pathname);
			
			int size = in.available();
			byte[] buffer = new byte[size];
			in.read(buffer);
			in.close();
			str = new String(buffer, "UTF-8");
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}

		return str;
	}

	// write file(Add to the last row)
	public static boolean Write(String filename, String str) {
		boolean b = true;
		try {
			BufferedWriter out = new BufferedWriter(new FileWriter(new File(filename), true));
			out.append(str);
			out.flush();
			out.close();
		} catch (IOException e) {
			e.printStackTrace();
			b = false;
		}
		return b;
	}

	// write file(Add to the start row)
	public static boolean Write_start(String filename, String str) {
		boolean b = true;
		if (!new File(filename).exists()) {
			CreateFile.createFile(filename);
		}
		try {
			BufferedWriter out = new BufferedWriter(new FileWriter(new File(filename), false));
			out.append(str);
			out.flush();
			out.close();
		} catch (IOException e) {
			e.printStackTrace();
			b = false;
		}
		return b;
	}
	
	
	public static String ReadValidateCode(String filepath,String mac) {
		String validateCode="";
		String licensestr=RWfile.Read(filepath);
		String[] str1=licensestr.split("\r\n");
		for(int i=0;i<str1.length;i++) {
			if(!str1[i].equals("") && str1[i].contains("=")) {
				String[] str2=str1[i].split("\t");
				String Mac=str2[0].split("= ")[1];
				Mac=Mac.toUpperCase();
				Mac=Mac.replace(":", "");
				Mac=Mac.replace("-", "");
				if(Mac.equals(mac)) {
					validateCode=str2[1].split("= ")[1];
				}
			}
		}
		return validateCode;
	}
	
	public static String ReadMac(String filepath) {
		String filemac="";
		String licensestr=RWfile.Read(filepath);
		String[] str1=licensestr.split("\r\n");
		for(int i=0;i<str1.length;i++) {
			if(!str1[i].equals("") && str1[i].contains("=")) {
				String[] str2=str1[i].split("\t");
				filemac=str2[0].split("= ")[1];
				filemac=filemac.toUpperCase();
				filemac=filemac.replace(":", "");
				filemac=filemac.replace("-", "");
			}
		}
		return filemac;
	}

}
