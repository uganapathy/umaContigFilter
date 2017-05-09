
package us.kbase.umacontigfilter;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.annotation.Generated;
import com.fasterxml.jackson.annotation.JsonAnyGetter;
import com.fasterxml.jackson.annotation.JsonAnySetter;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonPropertyOrder;


/**
 * <p>Original spec-file type: FilterContigsParams</p>
 * 
 * 
 */
@JsonInclude(JsonInclude.Include.NON_NULL)
@Generated("com.googlecode.jsonschema2pojo")
@JsonPropertyOrder({
    "assembly_input_ref",
    "workspace_name",
    "min_length",
    "libfile_args"
})
public class FilterContigsParams {

    @JsonProperty("assembly_input_ref")
    private String assemblyInputRef;
    @JsonProperty("workspace_name")
    private String workspaceName;
    @JsonProperty("min_length")
    private Long minLength;
    @JsonProperty("libfile_args")
    private List<LibfileArgsType> libfileArgs;
    private Map<String, Object> additionalProperties = new HashMap<String, Object>();

    @JsonProperty("assembly_input_ref")
    public String getAssemblyInputRef() {
        return assemblyInputRef;
    }

    @JsonProperty("assembly_input_ref")
    public void setAssemblyInputRef(String assemblyInputRef) {
        this.assemblyInputRef = assemblyInputRef;
    }

    public FilterContigsParams withAssemblyInputRef(String assemblyInputRef) {
        this.assemblyInputRef = assemblyInputRef;
        return this;
    }

    @JsonProperty("workspace_name")
    public String getWorkspaceName() {
        return workspaceName;
    }

    @JsonProperty("workspace_name")
    public void setWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
    }

    public FilterContigsParams withWorkspaceName(String workspaceName) {
        this.workspaceName = workspaceName;
        return this;
    }

    @JsonProperty("min_length")
    public Long getMinLength() {
        return minLength;
    }

    @JsonProperty("min_length")
    public void setMinLength(Long minLength) {
        this.minLength = minLength;
    }

    public FilterContigsParams withMinLength(Long minLength) {
        this.minLength = minLength;
        return this;
    }

    @JsonProperty("libfile_args")
    public List<LibfileArgsType> getLibfileArgs() {
        return libfileArgs;
    }

    @JsonProperty("libfile_args")
    public void setLibfileArgs(List<LibfileArgsType> libfileArgs) {
        this.libfileArgs = libfileArgs;
    }

    public FilterContigsParams withLibfileArgs(List<LibfileArgsType> libfileArgs) {
        this.libfileArgs = libfileArgs;
        return this;
    }

    @JsonAnyGetter
    public Map<String, Object> getAdditionalProperties() {
        return this.additionalProperties;
    }

    @JsonAnySetter
    public void setAdditionalProperties(String name, Object value) {
        this.additionalProperties.put(name, value);
    }

    @Override
    public String toString() {
        return ((((((((((("FilterContigsParams"+" [assemblyInputRef=")+ assemblyInputRef)+", workspaceName=")+ workspaceName)+", minLength=")+ minLength)+", libfileArgs=")+ libfileArgs)+", additionalProperties=")+ additionalProperties)+"]");
    }

}
