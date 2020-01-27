create table user(
    user_id integer primary key not null,
    user_name varchar(100)
    UNIQUE ("title") ON CONFLICT ABORT
);

create table audio(
    audio_id integer primary key not null,
    audio varchar(300)
);

create table user_audio(
    ua_id integer primary key not null,
    ua_user integer not null,
    ua_audio integer not null,
    foreign key (ua_user) references user(user_id),
    foreign key (ua_audio) references audio(audio_id)
);