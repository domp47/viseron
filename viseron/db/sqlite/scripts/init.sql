CREATE TABLE ffmpeg_log_level ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	name                 varchar(100) NOT NULL  UNIQUE  ,
	value                varchar(100) NOT NULL    
 );

CREATE TABLE pix_fmt ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	name                 varchar(100) NOT NULL    ,
	value                varchar(100) NOT NULL    
 );

CREATE TABLE rtsp_protocol ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	name                 varchar(100) NOT NULL    ,
	value                varchar(100) NOT NULL    
 );

CREATE TABLE stream_format ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	name                 varchar(100) NOT NULL    ,
	value                varchar(100) NOT NULL    
 );

CREATE TABLE updates ( 
	name                 varchar(100) NOT NULL  PRIMARY KEY  ,
	date                 datetime  DEFAULT CURRENT_TIMESTAMP   
 );

CREATE TABLE viseron_log_level ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	name                 varchar(100) NOT NULL    ,
	value                varchar(100) NOT NULL    
 );

CREATE TABLE camera ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	name                 varchar(100) NOT NULL    ,
	mqtt_name            varchar(100) NOT NULL    ,
	stream_format_id     integer NOT NULL    ,
	host                 varchar(100) NOT NULL    ,
	port                 integer NOT NULL    ,
	username             varchar(100)     ,
	password             varchar(100)     ,
	width                integer     ,
	height               integer     ,
	fps                  integer     ,
	global_args          varchar(100)     ,
	input_args           varchar(100)     ,
	hwaccel_args         varchar(100)     ,
	codec                varchar(100)     ,
	audio_codec          varchar(100)     ,
	rtsp_transport_id    integer NOT NULL    ,
	filter_args          varchar(100)     ,
	frame_timeout        varchar(100)     ,
	pix_fmt_id           integer     ,
	substream_stream_format_id integer     ,
	substream_port       integer     ,
	substream_path       varchar(100)     ,
	substream_width      integer     ,
	substream_height     integer     ,
	substream_fps        varchar(100)     ,
	substream_input_args varchar(100)     ,
	substream_hwaccel_args varchar(100)     ,
	substream_codec      varchar(100)     ,
	substream_audio_codec varchar(100)     ,
	substream_rtsp_transport_id integer     ,
	substream_filter_args varchar(100)     ,
	substream_frame_timeout integer     ,
	substream_pix_fmt_id integer     ,
	motion_interval      double NOT NULL    ,
	motion_trigger_detector bit NOT NULL    ,
	motion_trigger_recorder bit NOT NULL    ,
	motion_timeout       bit NOT NULL    ,
	motion_max_timeout   integer NOT NULL    ,
	motion_width         integer NOT NULL    ,
	motion_height        integer NOT NULL    ,
	motion_frames        integer NOT NULL    ,
	motion_log_level_id  integer NOT NULL    ,
	object_enabled       bit NOT NULL    ,
	object_interval      integer     ,
	object_labels        varchar(100)     ,
	object_log_all_objects bit     ,
	object_max_frame_age double     ,
	object_log_level_id  integer     ,
	publish_image        bit NOT NULL    ,
	ffmpeg_log_level_id   integer     ,
	ffmpeg_recoverable_errors varchar(100)     ,
	ffprobe_log_level_id  integer     ,
	log_level_id         integer     ,
	FOREIGN KEY ( stream_format_id ) REFERENCES stream_format( id )  ,
	FOREIGN KEY ( rtsp_transport_id ) REFERENCES rtsp_protocol( id )  ,
	FOREIGN KEY ( pix_fmt_id ) REFERENCES pix_fmt( id )  ,
	FOREIGN KEY ( substream_pix_fmt_id ) REFERENCES pix_fmt( id )  ,
	FOREIGN KEY ( substream_stream_format_id ) REFERENCES stream_format( id )  ,
	FOREIGN KEY ( substream_rtsp_transport_id ) REFERENCES rtsp_protocol( id )  ,
	FOREIGN KEY ( ffmpeg_log_level_id ) REFERENCES ffmpeg_log_level( id )  ,
	FOREIGN KEY ( ffprobe_log_level_id ) REFERENCES ffmpeg_log_level( id )  ,
	FOREIGN KEY ( log_level_id ) REFERENCES viseron_log_level( id )  ,
	FOREIGN KEY ( object_log_level_id ) REFERENCES viseron_log_level( id )  ,
	FOREIGN KEY ( motion_log_level_id ) REFERENCES viseron_log_level( id )  
 );

CREATE TABLE mask ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	camera_id            integer NOT NULL    ,
	FOREIGN KEY ( camera_id ) REFERENCES camera( id ) ON DELETE CASCADE ON UPDATE CASCADE
 );

CREATE TABLE mask_point ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	mask_id              integer NOT NULL    ,
	x                    integer NOT NULL    ,
	y                    integer NOT NULL    ,
	FOREIGN KEY ( mask_id ) REFERENCES mask( id ) ON DELETE CASCADE ON UPDATE CASCADE
 );

CREATE TABLE recording ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	camera_id            integer NOT NULL    ,
	time                 datetime NOT NULL    ,
	filename            varchar(100)     ,
	FOREIGN KEY ( camera_id ) REFERENCES camera( id ) ON DELETE CASCADE ON UPDATE CASCADE
 );

CREATE TABLE static_mjpeg_stream ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	camera_id            integer NOT NULL    ,
	width                integer     ,
	height               integer     ,
	draw_objects         bit     ,
	draw_motion          bit     ,
	draw_motion_mask     bit     ,
	draw_object_mask     bit     ,
	draw_zones           bit     ,
	rotate               integer     ,
	mirror               bit     ,
	FOREIGN KEY ( camera_id ) REFERENCES camera( id ) ON DELETE CASCADE ON UPDATE CASCADE
 );

CREATE TABLE zone ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	camera_id            integer NOT NULL    ,
	labels               varchar(100)     ,
	FOREIGN KEY ( camera_id ) REFERENCES camera( id ) ON DELETE CASCADE ON UPDATE CASCADE
 );

CREATE TABLE zone_point ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	zone_id              integer NOT NULL    ,
	x                    integer NOT NULL    ,
	y                    integer NOT NULL    ,
	FOREIGN KEY ( zone_id ) REFERENCES zone( id ) ON DELETE CASCADE ON UPDATE CASCADE
 );

CREATE TABLE motion_event ( 
	id                   integer NOT NULL  PRIMARY KEY autoincrement ,
	recording_id         integer NOT NULL    ,
	timestamp_start      varchar(32) NOT NULL    ,
	timestamp_end        varchar(32) NOT NULL    ,
	FOREIGN KEY ( recording_id ) REFERENCES recording( id ) ON DELETE CASCADE ON UPDATE CASCADE
 );


INSERT INTO stream_format (name, value)
VALUES
	('RTSP', 'rtsp'),
	('RTMP', 'rtmp'),
	('M-JPEG', 'mjpeg');

INSERT INTO rtsp_protocol (name, value)
VALUES
	('TCP', 'tcp'),
	('UDP', 'udp'),
	('UDP Multicast', 'udp_multicast'),
	('HTTP', 'http');

INSERT INTO pix_fmt (name, value)
VALUES
	('NV12', 'nv12'),
	('YUV 420P', 'yuv420p');

INSERT INTO ffmpeg_log_level (name, value)
VALUES
	('Quiet', 'quiet'),
	('Panic', 'panic'),
	('Fatal', 'fatal'),
	('Error', 'error'),
	('Warning', 'warning'),
	('Info', 'info'),
	('Verbose', 'verbose'),
	('Debug', 'debug'),
	('Trace', 'trace');

INSERT INTO viseron_log_level (name, value)
VALUES
	("Debug", "debug"),
	("Info", "info"),
	("Warning", "warning"),
	("Error", "error"),
	("Fatal", "fatal");

INSERT INTO updates (name)
VALUES ('init');