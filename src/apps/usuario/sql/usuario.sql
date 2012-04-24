ALTER TABLE `redesogcs`.`usuario` DROP PRIMARY KEY,
 ADD PRIMARY KEY  USING BTREE(`codigo`, `numero`);
insert into usuario(user_id,numero,nivel_id,organismo_id,dependencia,nombres,sexo,email,contrasena,emailalt,fono,anexo,celular,estado_id)
values(1,0,2,1,0,'Herald Olivares','MA','heraldmatias.oz@gmail.com','','heraldmatias.oz@gmail.com','4067881','1206','958059986',1);
