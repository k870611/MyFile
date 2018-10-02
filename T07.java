import java.io.*;

public class T07 {

	public static void main(String[] args) throws IOException,
				ClassNotFoundException {
		double n1 = -12345.6789;
		System.out.printf("%,-+(15.3f\n", n1);	
		
		
		
		Cat cat = new Cat("Hello Kitty",3);
		ObjectOutputStream oos = 
			new ObjectOutputStream(new FileOutputStream("ccc.bin"));
		oos.writeObject(cat);
		oos.close();
		System.out.printf("%s 寫檔成功...\n", "ccc.bin");
		
		ObjectInputStream ois = 
				new ObjectInputStream( new FileInputStream("ccc.bin"));
		
		Cat cat2 =  (Cat)ois.readObject();
		System.out.println( cat2.getName() +"---");
		
		
		
		DataOutputStream dos =
				new DataOutputStream( new FileOutputStream("bbb.bin"));
		int v1 = 123;
		long v2 = 456;
		double v3 = 678.678;
		String v4 = "Hello world";
		dos.writeInt(v1);
		dos.writeLong(v2);
		dos.writeDouble(v3);
		dos.writeUTF(v4);
		dos.close();
		
		DataInputStream dis =
				new DataInputStream( new FileInputStream("bbb.bin"));
		
		System.out.printf("v1=%d v2=%d v3=%.3f v4=%s\n",
			dis.readInt(),dis.readLong(),dis.readDouble(),dis.readUTF());
		dis.close();
		
		
		FileInputStream fis = 
				new FileInputStream("src/resource/III.png");
		FileOutputStream fos =
				new FileOutputStream("src/resource/III2.png");
		
		int b;
		while( ( b=fis.read() ) != -1 ){
			fos.write(b);			
		}
		fis.close();
		fos.close();
		System.out.printf("%s 寫檔成功...\n", "III2.png");
		
		
		
		String fname = "aaa.txt";
		//FileWriter fw = new FileWriter(fname);
		BufferedWriter fw = new BufferedWriter( new FileWriter(fname) );
		
		//File f = new File(fname);
		//f.exists();
		//f.mkdirs();		
		//FileWriter fw = new FileWriter(f);
		
		fw.write("小甜甜\r\n鐵雄\r\n");
		fw.write("Hello Kitty\r\n");
		fw.write('A');
		char[] chars = {'A','B','大','牛','\r','\n'};
		fw.write(chars);
		fw.close();
		System.out.printf("%s 寫檔成功...\n", fname);
		
		
		//FileReader fr = new FileReader(fname);
		BufferedReader fr = new BufferedReader(new FileReader(fname));
		int ch;
		while((ch=fr.read()) != -1){
			//System.out.print((char)ch);
			System.out.printf("%c", ch);
		}
				
		fr.close();

	}

}













