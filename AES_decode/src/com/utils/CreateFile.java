package com.utils;

import java.io.File;

public class CreateFile {

	public static boolean createFile(String filepath) {
		try{
			File dir=new File(filepath); 
			if(!dir.exists()) {
				dir.createNewFile(); 
				return true;
			}
		}catch(Exception e){
			  e.printStackTrace();  
			} 
		return false;
	}
	
}
