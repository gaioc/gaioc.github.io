<html>
  <?php
    $command = escapeshellcmd('create_user.py {$_POST["username"]} {$_POST["password"]}');
    $output = shell_exec($command);
    echo $output
  ?>
</html>
