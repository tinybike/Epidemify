<?php
// Convert SQL datetime to a more readable format
function processDateTime($sqldatetime) {
	list($yyyy, $mm, $dd_time) = explode('-', $sqldatetime);
	list($dd, $time) = explode(' ', $dd_time);
	$dd = strval(intval($dd + 0));
	$mm = strval(intval($mm + 0));
	list($hour, $min, $sec) = explode(':', $time);
	$ampm = 'AM';
	$hour = strval(intval($hour));
	if (intval($hour) >= 12) {
		if (intval($hour) > 12) {
			$hour = strval(intval($hour) - 12);
		}
		/*else {
			$hour = strval(intval($hour));
		}*/
		$ampm = 'PM';
	}
	return array($yyyy, $mm, $dd, $hour, $min, $sec, $ampm);
}
function processDateTimeMM($sqldatetime, $mm_format) {
	$months = array('01' => 'January', '02' => 'February', '03' => 'March', 
					'04' => 'April', '05' => 'May', '06' => 'June',
					'07' => 'July', '08' => 'August', '09' => 'September',
					'10' => 'October', '11' => 'November', '12' => 'December');
	list($yyyy, $mm, $dd_time) = explode('-', $sqldatetime);
	list($dd, $time) = explode(' ', $dd_time);
	$dd = strval(intval($dd + 0));
	$mm = strval(intval($mm + 0));
	if ($mm_format == 1) {
		$mm = $months[$mm];
	}
	list($hour, $min, $sec) = explode(':', $time);
	$ampm = 'AM';
	$hour = strval(intval($hour));
	if (intval($hour) >= 12) {
		if (intval($hour) > 12) {
			$hour = strval(intval($hour) - 12);
		}
		/*else {
			$hour = strval(intval($hour));
		}*/
		$ampm = 'PM';
	}
	return array($yyyy, $mm, $dd, $hour, $min, $sec, $ampm);
}

// Convert PHP datetime to SQL format & human-readable format
function processPHPDateTime($phpdatetime) {
    list($mm, $dd, $yyyyhhmm) = explode('/', $phpdatetime);
	list($yyyy, $hhmm) = explode(' ', $yyyyhhmm);
	$sqldatetime = $yyyy . '-' . $mm . '-' . $dd . ' ' . $hhmm . ':00';
	list($dd_yyyy, $dd_mm, $dd_dd, $dd_hour, $dd_min, $dd_sec, $dd_ampm) = processDateTime($sqldatetime);
	$hdatetime = $dd_mm.'/'.$dd_dd.'/'.$dd_yyyy.' at '.$dd_hour.':'.$dd_min.' '.$dd_ampm;
	return array($sqldatetime, $hdatetime);
}
