<html>
  <?php
    $command = escapeshellcmd('create_user.py');
    $output = shell_exec($command);
    echo $output
  ?>
</html>
