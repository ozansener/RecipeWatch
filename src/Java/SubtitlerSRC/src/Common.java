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
 * @version "0.6, 08/11/13"
 */

public class Common {
    public static String getExtension(String filename) {
        String extension;
        int i;
        
        extension = null;
        if (filename == null)
            return null;
        i = filename.lastIndexOf(".");
        if ((i > 0) && (i < filename.length() - 1))
            extension = filename.substring(i+1).toLowerCase();
        
        return extension;
    }

    public static String removeExtension(String filename) {
        String noExtension;
        int i;
        
        noExtension = filename;
        i = filename.lastIndexOf(".");
        if ((i > 0) && (i < filename.length() - 1))
            noExtension = filename.substring(0, i);
        
        return noExtension;
    }
}
