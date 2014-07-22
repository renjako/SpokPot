<?php

function getcwd_spok() {
	return '/var/www';
}

function getmygid_spok() {
	return '0';
}

function is_writable_spok() {
	return true;
}

function function_exists_spok() {
	return true;
}

function disk_free_space_spok() {
	return '36698988544';
}

function system_spok($cmd, $ret) {
	if ($cmd == 'id') {
		$ret = array('uid=0(root) gid=0(root) groups=0(root)',);
	}
	elseif ($cmd == 'uptime') {
		$ret = array('16:12:55 up 152 days, 19:03,  0 user,  load average: 0.02, 0.02, 0.03',);
	}
	else {
		$ret = array('None',);
	}
}

function exec_spok($cmd, $ret) {
	if ($cmd == 'id') {
		$ret = array('uid=0(root) gid=0(root) groups=0(root)',);
	}
	else {
		$ret = array('None',);
	}
}

function php_uname_spok() {
	return 'Linux Server 2.6.38-11-generic #49-Ubuntu SMP Mon Aug 29 20:47:58 UTC 2011 i686';
}

function disk_total_space_spok() {
	return '51221590016';
}

function shell_exec_spok($cmd) {
	if ($cmd == 'id') {
		$ret = array('uid=0(root) gid=0(root) groups=0(root)',);
	}
	else {
		$ret = array('None',);
	}
	return $ret;
}

function passthru_spok($cmd, $ret) {
	if ($cmd == 'id') {
		$ret = array('uid=0(root) gid=0(root) groups=0(root)',);
	}
	else {
		$ret = array('None',);
	}
}

function get_current_user_spok() {
	return 'root';
}

function fsockopen_spok() {
	return false;
}

function getenv_spok($varname) {
	$ret = "";
	return $ret;
}

function getmyuid_spok() {
	return '0';
}

function diskfreespace_spok() {
	return '36698988544';
}

function ini_get_spok($varname) {
	if ($varname == 'save_mode') {
		$ret = 'None';
	}
	elseif ($varname == 'disable_functions') {
		$ret = 'None';
	}
	else {
		$ret = 'None';
	}
}

function is_callable_spok() {
	return true;
}

function popen_spok($cmd) {
	if ($cmd == 'id') {
		$temp = tmpfile();
		fwrite($temp, 'uid=0(root) gid=0(root) groups=0(root)');
		$ret = $temp;
	}
	else {
		$ret = tmpfile();
	}
	return $ret;
}

include $argv[1];
?>
