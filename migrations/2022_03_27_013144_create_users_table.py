from orator.migrations import Migration


class CreateUsersTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.create('users') as table:
            table.increments('id')
            table.string('nombres', 30)
            table.string('apellidos', 40)
            table.string('puesto', 30)
            table.string('user', 20)
            table.string('password')
            table.string('access')
            table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        self.schema.drop('users')
