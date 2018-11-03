package com.utils;

import java.util.ArrayList;
import java.util.Random;

public class ProcessStr {

    public static String getCharAndNumr(int length) {
        String val = "";
        Random random = new Random();
        for (int i = 0; i < length; i++) {
            String charOrNum = random.nextInt(2) % 2 == 0 ? "char" : "num";
            if ("char".equalsIgnoreCase(charOrNum)) {
                int choice = random.nextInt(2) % 2 == 0 ? 65 : 97;
                val += (char) (choice + random.nextInt(26));
            } else if ("num".equalsIgnoreCase(charOrNum)) { 
                val += String.valueOf(random.nextInt(10));
            }
        }
        return val;
    }

	public static ArrayList<Integer> getNumArray(String str) {
    	str=str.trim();
    	ArrayList<Integer> list=new ArrayList<Integer>();
    	if(str != null && !"".equals(str)){
	    	for(int i=0;i<str.length();i++){
		    	if(str.charAt(i)>=48 && str.charAt(i)<=57){
		    		int n=str.charAt(i)-48;
		    		Integer nn=new Integer(n);
		    		list.add(nn);
		    	}
	    	}
    	}
    	return list;
	}

    
}
