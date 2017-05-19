import java.util.HashSet;
import java.util.Set;

import org.eclipse.core.resources.IProject;
import org.eclipse.core.runtime.IProgressMonitor;
import org.eclipse.core.runtime.NullProgressMonitor;
import org.eclipse.jdt.core.IClasspathEntry;
import org.eclipse.jdt.core.IJavaProject;

public class Entries {

	private Set<IClasspathEntry> entries;
	private IProject projet;
	private IJavaProject javaProject;
	private IProgressMonitor progressMonitor;
	
	 public Entries(IProject project)
	 {
		 this.entries = new HashSet<IClasspathEntry>();
		 this.projet = project;
		 this.javaProject = null;
		 this.progressMonitor = new NullProgressMonitor();
	 }
	
	public Set<IClasspathEntry> getEntries() {
		return entries;
	}

	public void setEntries(Set<IClasspathEntry> entries) {
		this.entries = entries;
	}

	public IProject getProject() {
		return projet;
	}

	public void setProject(IProject project) {
		this.projet = project;
	}


	public IJavaProject getJavaProject() {
		return javaProject;
	}

	public void setJavaProject(IJavaProject javaProject) {
		this.javaProject = javaProject;
	}

	public IProgressMonitor getProgressMonitor() {
		return progressMonitor;
	}

	public void setProgressMonitor(IProgressMonitor progressMonitor) {
		this.progressMonitor = progressMonitor;
	}
}
