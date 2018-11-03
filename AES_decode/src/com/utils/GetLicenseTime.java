package com.utils;

import java.io.File;
import java.text.DateFormat;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;

public class GetLicenseTime {

//	public static int GetLicenseTime(String folder) {
//		String filename = folder + "/License";
//		String startTime = getLastModifiedTime(filename);
//		String endTime = getCurrentDate("yyyy-MM-dd");
//		int day = compareDate(startTime, endTime, 0);
//		return day;
//	}

	public static String getLastModifiedTime(String filepath) {
		File file = new File(filepath);
		long time = file.lastModified();
		String ctime = new SimpleDateFormat("yyyy-MM-dd").format(new Date(time));
		return ctime;
	}

	public static String getCurrentDate(String format) {
		Calendar day = Calendar.getInstance();
		day.add(Calendar.DATE, 0);
		SimpleDateFormat sdf = new SimpleDateFormat(format);
		String date = sdf.format(day.getTime());
		return date;
	}

	// stype: return value type, 0->day,1->month,2->year
	public static int compareDate(String startDay, String endDay, int stype) {
		int n = 0;
		String formatStyle = stype == 1 ? "yyyy-MM" : "yyyy-MM-dd";

		endDay = endDay == null ? getCurrentDate("yyyy-MM-dd") : endDay;

		DateFormat df = new SimpleDateFormat(formatStyle);
		Calendar c1 = Calendar.getInstance();
		Calendar c2 = Calendar.getInstance();
		try {
			c1.setTime(df.parse(startDay));
			c2.setTime(df.parse(endDay));
		} catch (Exception e3) {
			System.out.println("License wrong occured");
		}
		while (!c1.after(c2)) {
			n++;
			if (stype == 1) {
				c1.add(Calendar.MONTH, 1);
			} else {
				c1.add(Calendar.DATE, 1);
			}
		}
		n = n - 1;
		if (stype == 2) {
			n = (int) n / 365;
		}
		return n;
	}

}
