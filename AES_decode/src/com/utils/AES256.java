package com.utils;


  
import java.io.UnsupportedEncodingException;
import java.security.Security;
import java.util.Arrays;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;  
  

  
public class AES256 {  
  
	private static final String DEFAULT_CIPHER_ALGORITHM = "AES/CBC/PKCS7Padding";

    public static String encrypt(String content, String password) {
   
        try {
	        SecretKeySpec skeySpec = getKey(password);
	        byte[] clearText = content.getBytes("UTF8");
	        final byte[] iv = new byte[16];
	        Arrays.fill(iv, (byte) 0x00);
	        IvParameterSpec ivParameterSpec = new IvParameterSpec(iv);
	        
	        Security.addProvider(new org.bouncycastle.jce.provider.BouncyCastleProvider());
	        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS7Padding");
	        cipher.init(Cipher.ENCRYPT_MODE, skeySpec, ivParameterSpec);
	        
	        String encrypedValue = Base64.encodeToString(cipher.doFinal(clearText), Base64.DEFAULT);
	        return encrypedValue;
        } catch (Exception ex) {
        	ex.printStackTrace();
        }
        return null;
    }

  
    public static String decrypt(String content, String password){
        try {
	        SecretKey key = getKey(password);
	        final byte[] iv = new byte[16];
	        Arrays.fill(iv, (byte) 0x00);
	        IvParameterSpec ivParameterSpec = new IvParameterSpec(iv);
	        
	        byte[] encrypedPwdBytes = Base64.decode(content, Base64.DEFAULT);
	        Security.addProvider(new org.bouncycastle.jce.provider.BouncyCastleProvider());
	        Cipher cipher = Cipher.getInstance(DEFAULT_CIPHER_ALGORITHM);
	        cipher.init(Cipher.DECRYPT_MODE, key, ivParameterSpec);
	        byte[] decrypedValueBytes = (cipher.doFinal(encrypedPwdBytes));
	        
	        String decrypedValue = new String(decrypedValueBytes , "UTF-8");
	        return decrypedValue;
        } catch (Exception ex) {
//        	ex.printStackTrace();
        }
        return null;
    }
    
	private static SecretKeySpec getKey(String password) throws UnsupportedEncodingException {
	    int keyLength = 256;
	    byte[] keyBytes = new byte[keyLength / 8];
	    Arrays.fill(keyBytes, (byte) 0x0);
	    
	    byte[] passwordBytes = password.getBytes("UTF-8");
	    int length = passwordBytes.length < keyBytes.length ? passwordBytes.length : keyBytes.length;
	    System.arraycopy(passwordBytes, 0, keyBytes, 0, length);
	    SecretKeySpec key = new SecretKeySpec(keyBytes, "AES");
	    return key;
	}


      
}  
