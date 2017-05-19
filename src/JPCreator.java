import org.eclipse.core.resources.IProject;
import org.eclipse.core.resources.IProjectDescription;
import org.eclipse.core.resources.IWorkspaceRoot;
import org.eclipse.core.resources.ResourcesPlugin;
import org.eclipse.core.runtime.CoreException;
import org.eclipse.core.runtime.IProgressMonitor;
import org.eclipse.jdt.core.IClasspathEntry;
import org.eclipse.jdt.core.JavaCore;
import org.eclipse.jdt.core.JavaModelException;
import org.eclipse.jdt.launching.JavaRuntime;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.net.URL;
import java.nio.channels.Channels;
import java.nio.channels.ReadableByteChannel;

public class JPCreator {

	public void createJavaSrcFolder(Entries entries) {
		new File(entries.getProject().getLocation().toString() + "/src").mkdirs();
		entries.getEntries().add(JavaCore.newSourceEntry(entries.getProject().getFullPath().append("src")));
	}

	public Entries createJavaProject(String project_name) throws CoreException {
		IWorkspaceRoot root = ResourcesPlugin.getWorkspace().getRoot();
		IProject project = root.getProject(project_name);
		Entries entries = new Entries(project);
		IProgressMonitor progressMonitor = entries.getProgressMonitor();
		project.create(progressMonitor);
		project.open(progressMonitor);

		// Creating JavaProject
		IProjectDescription description = project.getDescription();
		String[] natures = description.getNatureIds();
		String[] newNatures = new String[natures.length + 1];
		System.arraycopy(natures, 0, newNatures, 0, natures.length);
		newNatures[natures.length] = JavaCore.NATURE_ID;
		description.setNatureIds(newNatures);
		project.setDescription(description, progressMonitor);
		entries.setJavaProject(JavaCore.create(project));

		// Adding dependenciess
		entries.getEntries().add(JavaRuntime.getDefaultJREContainerEntry());
		entries.getJavaProject().setRawClasspath(
				entries.getEntries().toArray(new IClasspathEntry[entries.getEntries().size()]), progressMonitor);
		entries.getProject().refreshLocal(0, entries.getProgressMonitor());
		return entries;
	}

	public void createJavaDependencies(Entries entries, String libraryName) throws JavaModelException {
		entries.getEntries()
				.add(JavaCore.newLibraryEntry(entries.getProject().getFullPath().append(libraryName), null, null));
		entries.getJavaProject().setRawClasspath(
				entries.getEntries().toArray(new IClasspathEntry[entries.getEntries().size()]),
				entries.getProgressMonitor());

	}

	public String downloadFile(String url, Entries entries, String nom) throws IOException {
		FileOutputStream fos = null;
		URL website = new URL(url);
		ReadableByteChannel rbc = Channels.newChannel(website.openStream());
		fos = new FileOutputStream(entries.getProject().getLocation().toString() + "/" + nom);
		fos.getChannel().transferFrom(rbc, 0, Long.MAX_VALUE);
		System.out.println("Download complete!");
		fos.close();
		return nom;
	}

}
