/*
    This file is part of Google2SRT.

    Google2SRT is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    Google2SRT is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Google2SRT.  If not, see <http://www.gnu.org/licenses/>.
 */

/**
 *
 * @author kom
 * @version "0.4, 09/06/08"
 */

import java.io.File;
import javax.swing.filechooser.*;

public class XMLFilter extends FileFilter {
    final String acc = "xml";
    
    public boolean accept(File f) {
        String ext;
        if (f.isDirectory())
            return true;
        ext = Common.getExtension(f.getName());
        return acc.equals(ext);
    }

    public String getDescription() {
        return "XML (*.xml)";
    }

}
