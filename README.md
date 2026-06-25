TRABAJO PRÁCTICO FINAL – GRUPO 3 Programacion Avanzada

Integrantes: Catalina Lannegrasse, Gonzalo Cardenas , Ivan Molina , Ariel Arce.

Descripción del Sistema
Este proyecto es un sistema de gestión para una biblioteca digital desarrollado en Python utilizando el paradigma de Programación Orientada a Objetos (POO). El software permite administrar de forma eficiente el catálogo de libros, el registro de usuarios con diferentes niveles de acceso, y el flujo completo de préstamos y devoluciones.

Características y Decisiones de Diseño:
* Gestión Completa (ABML): Permite el alta, baja, modificación y listado tanto de libros como de clientes, incluyendo validaciones para evitar ISBNs duplicados.
* Metaclases y Polimorfismo: Se utiliza una metaclase (`MetaPersona`) para asegurar que todos los usuarios implementen obligatoriamente el método `mostrar_rol()`, diferenciando los permisos entre Clientes y Administradores.
* Patrón Factory Method: Implementado en la clase `UsuarioFactory` para centralizar y desacoplar la creación de los distintos tipos de usuarios.
* Decoradores: Se diseñó un decorador personalizado (`@validar_correo`) que audita y restringe el formato de los emails antes de guardarlos en el sistema.
* Arquitectura UML: El diseño separa estrictamente las relaciones de Agregación (libros y clientes independientes) y Composición (los registros de préstamos, que dependen del ciclo de vida de la biblioteca).

Consigna General

Desarrollar una aplicación en Python denominada Sistema de Gestión de Biblioteca Digital. El sistema deberá permitir administrar libros, usuarios y préstamos utilizando Programación Orientada a Objetos.

Requerimientos Funcionales

Gestión de Libros

Datos mínimos: Título, Autor, ISBN, Año de publicación y Cantidad de páginas.
Operaciones mínimas: Alta, Modificación, Baja y Listado.

Gestión de Usuarios

Datos mínimos: Nombre, Apellido, DNI y Correo electrónico.
Operaciones mínimas: Alta, Modificación, Baja y Listado.

Gestión de Préstamos

Registrar préstamos, devoluciones y consultar préstamos activos.
Un libro no podrá prestarse si ya posee un préstamo activo.
Se deberá registrar fecha de préstamo y devolución.

Requerimientos Técnicos

• Implementar al menos una jerarquía de herencia.
• Implementar al menos un comportamiento polimórfico.
• Implementar al menos una relación de agregación.
• Implementar al menos una relación de composición.
• Implementar al menos un decorador propio e integrarlo dentro del sistema.
• Implementar una metaclase utilizando type o una clase derivada de type.
• Implementar al menos un patrón de diseño, debidamente justificado.

Diagrama UML

El trabajo deberá incluir un diagrama UML completo que represente: Clases Atributos Métodos principales Relaciones de herencia Relaciones de agregación Relaciones de composición
