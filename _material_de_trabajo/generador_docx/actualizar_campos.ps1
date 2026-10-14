$docPath = 'C:\Users\SISTEMAS10\Desktop\Estudio\TESIS NUEVA\Avance de tesis.docx'
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open($docPath)
    Write-Host 'Actualizando campos...'
    $doc.Fields.Update()
    foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
    foreach ($tof in $doc.TablesOfFigures) { $tof.Update() }
    $doc.Save()
    $doc.Close()
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
    Write-Host 'Documento actualizado con éxito.'
} catch {
    Write-Host "Error en COM: $($_.Exception.Message)"
}
