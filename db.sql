create table user(
    user_name varchar(100) primary key not null
);

create table audio(
    audio varchar(100) primary key not null
);

create table photo(
    photo varchar(100) primary key
);

create table user_photo(
    up_id integer primary key not null,
    up_user varchar(100) not null,
    up_photo varchar(100) not null,
    foreign key (up_user) references user(user_name),
    foreign key (up_photo) references photo(photo)
);

create table user_audio(
    ua_id integer primary key not null,
    ua_user integer not null,
    ua_audio integer not null,
    foreign key (ua_user) references user(user_name),
    foreign key (ua_audio) references audio(audio)
);